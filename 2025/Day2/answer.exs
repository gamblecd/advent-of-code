defmodule Day do
  Code.require_file("utils/util.ex")

  def impl(lines, checker) do
    total_count = Enum.reduce(String.split(Enum.at(lines, 0), ","), 0, fn range, count ->
      unless range == "" do
        ends = String.split(range, "-")
        start = String.to_integer(Enum.at(ends, 0))
        end_num = String.to_integer(Enum.at(ends, 1))
        Enum.reduce(start..end_num, count, fn num, acc ->
          if checker.(num) do
            acc + num
          else
            acc
          end
        end)
      end
    end)
    total_count
  end

  def is_repeated(number) do
    str_number = Integer.to_string(number)
    length = String.length(str_number)
    if rem(length, 2) == 1 do
      false
    else
      split = div(length, 2)
      rem(number, Integer.pow(10, split)) == div(number, Integer.pow(10, split))
    end
  end

  def faster_has_repeated_sequence(number) do
    str_num = Integer.to_string(number)
    len = String.length(str_num)

    if len <= 1 do
      false
    else
      doubled = str_num <> str_num
      middle  = String.slice(doubled, 1, 2 * len - 2)
      String.contains?(middle, str_num)
    end
  end

  def part1(lines) do
    impl(lines, &is_repeated/1)
  end

  def part2(lines) do
    impl(lines, &faster_has_repeated_sequence/1)
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
