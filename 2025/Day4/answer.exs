defmodule Day do
  Code.require_file("utils/util.ex")
  Code.require_file("utils/navigation.ex")

  def build_overlay(grid, func) do
    Util.reduce_grid(grid, %{}, fn value, {x,y}, grid, hash ->
      new_hash =
        if value == "@" do
          Map.put(hash,{x,y}, func.(grid, {x,y}))
        else
          hash
        end
      new_hash
    end)
  end

  def count_adjacent(grid, {x, y}) do
    count = Enum.reduce(Navigation.dirs(), 0, fn dir, acc ->
    # for each dir, check if in bounds, and then count if it's a @
      {new_x, new_y}= dir.({x,y})
      if Navigation.in_bounds({new_x, new_y}, {length(grid), length(Enum.at(grid, 0))}) do
        if get_index(grid, {new_x, new_y}) == "@" do
          acc + 1
        else
          acc
        end
      else
        acc
      end
    end)
    count
  end

  def get_index(grid, {x, y}) do
    Enum.at(grid, y) |> Enum.at(x)
  end

  def reduce_overlay(overlay, {x,y}) do
    {overlay, _x,_y} = Enum.reduce(Navigation.dirs(), {overlay, x,y}, fn dir, {overlay, x,y} ->
      pt = dir.({x,y})
      if Map.has_key?(overlay, pt) do
        v = Map.get(overlay, pt)
        {Map.put(overlay, pt, v-1), x,y}
      else
        {overlay, x,y}
     end
    end)
    overlay
  end

  def overlay_reduction(overlay, remove_count, recurse? \\ true) do
    {new_overlay, count} = Enum.reduce(overlay, {overlay, remove_count}, fn {k,v}, {overlay, remove_count} ->
      if v < 4 do
        acc = Map.delete(overlay, k)
        #IO.puts("Removing #{inspect(k)}, remove_count: #{remove_count}")
        {reduce_overlay(acc, k), remove_count+1}
      else
        {overlay, remove_count}
      end
    end)
    if count == remove_count do
      remove_count
    else
      if recurse? do
        overlay_reduction(new_overlay, count, recurse?)
      else
        count
      end
    end
  end

  def impl(overlay, recurse) do
    count = overlay_reduction(overlay, 0, recurse)
    count
  end

  def part1(overlay) do
    impl(overlay, false)
  end

  def part2(overlay) do
    impl(overlay, true)
  end

  # main entrypoint
  def main do
    lines = Util.get_input_lines(System.argv(), __ENV__.file() |> Path.dirname())
    overlay = build_overlay(Util.build_grid(lines), &count_adjacent/2)
    IO.puts("Part 1: #{part1(overlay)}")
    IO.puts("Part 2: #{part2(overlay)}")
  end
end

# Run main automatically when executed as a script
Day.main()
