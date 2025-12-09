defmodule Day do
  Code.require_file("utils/util.ex")
  Code.require_file("utils/navigation.ex")

  def find_start(grid) do
    Util.reduce_grid(grid, nil, fn (value, pt, _grid, acc) ->
      if acc != nil do
        acc
      else
        if value == "S" do
          pt
        else
          acc
        end
      end
    end)
  end

  def find_splitters(grid) do
     Util.reduce_grid(grid, [], fn (value, pt, _grid, acc) ->
        if value == "^" do
          acc ++ [pt]
        else
          acc
      end
    end)
  end

  def find_timeline(timelines, tachyon) do
    Enum.find(timelines, fn timeline ->
      Enum.member?(timeline, tachyon)
    end)
  end



  def traverse_tachyons(grid, tachyons, {seen_tachyons, timelines, split_count}) do
    # IO.puts("Level: #{split_count}")
    #IO.puts("Timelines: #{inspect(timelines)}")
    {tachyons, seen_tachyons, new_timelines, new_split_count} = Enum.reduce(tachyons, {MapSet.new(), seen_tachyons, %{}, 0}, fn tachyon, {acc, seen_tachyons, new_timelines, split_count} ->
      {new_tachs, new_split_count} = split(grid, tachyon)
      as_set = MapSet.new(new_tachs)
      new_timelines = Enum.reduce(new_tachs, new_timelines, fn new_tach, tms ->
        seen_timeline_count = Map.get(timelines, tachyon, 0) + Map.get(tms,new_tach, 0)
        #IO.puts("Seen timeline count: #{seen_timeline_count}")
        #IO.puts("Adding #{inspect(List.duplicate(tachyon, max(seen_timeline_count, 1)))} to timelines")
        tms = Map.put(tms, new_tach, max(seen_timeline_count, 1))
      end)
      #for every new tach add a timeline entry from the old tach with an increase in size
      {MapSet.union(acc, as_set), MapSet.union(seen_tachyons, as_set), new_timelines, split_count+new_split_count}
    end)
    if MapSet.size(tachyons) > 0 do
      traverse_tachyons(grid, tachyons, {seen_tachyons,  new_timelines , split_count+new_split_count})
    else
      {seen_tachyons, timelines, split_count}
    end
  end


  def impl(lines) do

    grid = Util.build_grid(lines)
    grid_size = {length(grid), length(Enum.at(grid, 0))}
    st = find_start(grid)
    splitters = find_splitters(grid)
    #Util.print_grid_basic(grid)
    tachyons = MapSet.new([st])
    {tachyons, timelines, split_count} = traverse_tachyons(grid, tachyons, {MapSet.new(), %{st => 1}, 0})
    Util.print_grid({0,0}, grid_size, ".", [{"|", tachyons}, {"^", splitters}, {"S", [st]}])
    IO.puts(Enum.sum(Map.values(timelines)))
    split_count


    # Enum.reduce(lines, 0, fn line, _count ->
    #   {:ok, line}
    # end)
  end

  #find start
  #navigate south
  # if split,
    # remove curr
    # add 2 starts


  def split(grid, pt) do
    if Navigation.in_bounds(pt, {length(grid), length(Enum.at(grid, 0))}) do
      if Util.get_index(grid, pt) == "^" do
        {[Navigation.east(Navigation.south(pt)), Navigation.west(Navigation.south(pt))], 1}
      else
        {[Navigation.south(pt)],0}
      end
    else
      {[], 0}
    end

  end

  #
  def part1(lines) do

    impl(lines)
  end

  def part2(lines) do
    impl(lines)
  end

  # main entrypoint
  def main do
    lines = Util.get_input_lines(System.argv(), __ENV__.file() |> Path.dirname())

    IO.puts("Part 1: #{part1(lines)}")
    IO.puts("Part 2: #{part2(lines)}")
  end
end

# Run main automatically when executed as a script
Day.main()
