defmodule Day do
  Code.require_file("utils/util.ex")

  def prep_line("", {ranges, ingredients, _space}) do
    {ranges, ingredients, true}
  end
  def prep_line(line, {ranges, ingredients, true}) do
    {ranges, ingredients ++ [String.to_integer(line)], true}
  end
  def prep_line(line, {ranges, ingredients, false}) do
    [first, second] = String.split(line, "-") |>Enum.map(&String.to_integer/1)
    {ranges ++ [{first, second}], ingredients, false}
  end

  def prep(lines) do
    Enum.reduce(lines, {[], [], false}, &prep_line/2)
  end

  def ingredient_fresh(fresh_ranges, ingredient) do
      Enum.any?(fresh_ranges, &in_range?(&1, ingredient))
  end

  def in_range?(range, value) do
    {first, second} = range
    value >= first and value <= second
  end

  def merge_range(range, range2, index) do
    {first, last} = range
    {r2_first, r2_last} = range2
      cond do
        in_range?(range2, first) and in_range?(range2, last) -> {range2, index}
        in_range?(range2, first) -> {{r2_first, last}, index}
        in_range?(range2, last) -> {{first, r2_last}, index}
        true -> nil
      end
  end

  def combine_ranges(ranges) do
    [first | rest] = Enum.sort(ranges)
    Enum.reduce(rest, [first], fn range, acc ->
      new_range = Enum.find_value(Enum.with_index(acc), nil, fn {range2, index} ->
        merge_range(range, range2, index)
      end)
      if new_range == nil do
        acc ++ [range]
      else
        {new_ranges, new_index} = new_range
        List.replace_at(acc, new_index, new_ranges)
      end
    end)
  end

  def count_space_in_ranges(ranges) do
    Enum.reduce(ranges, 0, fn {first, last}, acc ->
      acc + (last-first+1)
    end)
  end


  def part1(lines) do
    {ranges, ingredients, _} = prep(lines)
    Enum.count(ingredients, &ingredient_fresh(ranges, &1))
  end

  def part2(lines) do
    {ranges, _, _} = prep(lines)
    count_space_in_ranges(combine_ranges(ranges))
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
