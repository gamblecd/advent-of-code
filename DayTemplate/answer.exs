defmodule Day do
  @moduledoc false

  # Determine input file:
  # - if an argument is given: use that as the filename
  # - otherwise default to "actual.txt" in the same directory as the script
  def get_input_file do
    script_dir =
      __ENV__.file()
      |> Path.dirname()
      |> Path.join("inputs")

    case System.argv() do
      [filename | _] ->
        Path.join(script_dir, filename)
      [] ->
        Path.join(script_dir, "ex.txt")
    end
  end

  # prep() -> lines
  def prep(filename) do
    filename
    |> File.stream!()
    |> Stream.map(&String.trim/1)
    |> Enum.to_list()
  end

  # part1(lines)
  def part1(lines) do
    Enum.reduce(lines, 0, fn line, _count ->
      {:ok, line}
    end)
  end

  # part2(lines)
  def part2(lines) do
    Enum.reduce(lines, 0, fn line, _count ->
      {:ok, line}
    end)
  end

  # main entrypoint
  def main do
    lines = prep(get_input_file())

    IO.puts("Part 1:")
    IO.puts("\tAnswer: #{part1(lines)}")

    IO.puts("\nPart 2:")
    IO.puts("\tAnswer: #{part2(lines)}")
  end
end

# Run main automatically when executed as a script
Day.main()
