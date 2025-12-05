defmodule Day do
  Code.require_file("utils/util.ex")

  def impl(lines) do
    Enum.reduce(lines, 0, fn line, _count ->
      {:ok, line}
    end)
  end

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
