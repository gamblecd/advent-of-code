defmodule Day do
  Code.require_file("utils/util.ex")

  def joltage_of_array(line, {count, joltage}) do
    arr = String.graphemes(line) |> Enum.map(&String.to_integer/1)
    current_joltage = find_joltage(arr, joltage-1)
    {count + String.to_integer(current_joltage), joltage}
  end

  def impl(lines, joltage) do
    Enum.reduce(lines, {0, joltage}, &joltage_of_array/2)
  end

  def find_joltage(arr, joltage) do
    first = Enum.slice(arr, 0, length(arr)-joltage)
    # find the max of each array
    max_num = Enum.max(first)
    if joltage == 0 do
      Integer.to_string(max_num)
    else
      start = Enum.find_index(arr, fn x -> x == max_num end)
      last = Enum.slice(arr, start+1, length(arr)-start)
      Integer.to_string(max_num) <> find_joltage(last, joltage-1)
    end
  end


  def part1(lines) do
    {count, _joltage} = impl(lines, 2)
    count
  end

  def part2(lines) do
    {count, _joltage} = impl(lines, 12)
    count
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
