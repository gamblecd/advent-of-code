defmodule Day do
  Code.require_file("utils/util.ex")

  def build_junctions(lines) do
    Enum.reduce(lines, [], fn line, junctions ->
      pt = line
      |> String.split(",")
      |> Enum.map(fn x -> String.to_integer(x)  end) |> List.to_tuple()
      junctions ++ [pt]
    end)
  end

  def impl(lines, series \\ 10) do
    junctions = build_junctions(lines)
    distances = find_distances(junctions)
    circuits = Enum.map(junctions, fn pt -> [pt] end)
    {distances, circuits}
  end

  def distance3({x1, y1, z1}, {x2, y2, z2}) do
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    :math.sqrt(dx * dx + dy * dy + dz * dz)
  end

  def reduce_circuits(circuits, {pt,pt2}) do
    # find all circuits that contain pt or pt2
    # combine them into one circuit, and replace its location in the list
    cs = Enum.filter(circuits, fn circuit ->
      Enum.find(circuit, fn x -> x == pt or x == pt2 end)
    end)
    circuits = Enum.reduce(cs, circuits, fn c, circs ->
      List.delete(circs, c)
    end)
    c1 = List.flatten(cs)
    circuits = circuits ++ [c1]
    circuits

  end

  def join_circuit(distances, circuits, left \\ -1) do
    if (left == 0) do
        circuits
    else
      [{{pt, pt2}, distance} | rest] = distances
      circuits = reduce_circuits(circuits, {pt, pt2})
      if length(circuits) == 1 do
        {pt, pt2}
      else
        join_circuit(rest, circuits, left-1)
      end
    end
  end

  def find_distances(junctions) do
    distances = Enum.reduce(junctions, %{}, fn pt, acc ->
      acc = Enum.reduce(junctions, acc, fn pt2, acc2 ->
        acc2 = if pt == pt2 do
          acc2
        else
          if Map.has_key?(acc2, {pt,pt2}) or Map.has_key?(acc2, {pt2, pt}) do
            acc2
          else
            Map.put(acc2, {pt, pt2}, distance3(pt, pt2))
          end
        end
      end)
    end)
    Enum.map(distances, fn {k, v} ->
      {k,v}
    end) |> Enum.sort(fn {k1, v1}, {k2, v2} -> v1 < v2 end)
  end

  def find_top_3_sizes(circuits) do
    Enum.sort(circuits, fn x, y -> length(x) > length(y) end)
    |> Enum.take(3)
    |> Enum.map(fn x -> length(x) end)
  end

  def part2_solve({{x,_,_}, {x2,_,_}}) do
    x * x2
  end

  def part1({distances, circuits}) do
    circuits = join_circuit(distances, circuits, 1000)
    find_top_3_sizes(circuits) |> Enum.reduce(&*/2)
  end

  def part2({distances, circuits}) do
    {{x,_,_}, {x2,_,_}} = join_circuit(distances, circuits)
    x*x2
  end

  # main entrypoint
  def main do
    lines = Util.get_input_lines(System.argv(), __ENV__.file() |> Path.dirname())
    {distances, circuits} = impl(lines)
    IO.puts("Part 1: #{part1({distances, circuits})}")
    IO.puts("Part 2: #{part2({distances, circuits})}")
  end
end

# Run main automatically when executed as a script
Day.main()
