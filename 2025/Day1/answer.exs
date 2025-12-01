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
        Path.join(script_dir, "ex1.txt")
    end
  end

  # prep() -> lines
  def prep(filename) do
    filename
    |> File.stream!()
    |> Stream.map(&String.trim/1)
    |> Enum.to_list()
  end

  def mod_rotate(current, amount, direction) do
    next =
      cond do
        direction == "L" -> current - amount
        true -> current + amount
      end
    counter =
      cond do
        current == 0 -> 0
        next <= 0 -> 1
        true -> 0
      end
    {div(abs(next), 100)+counter, Integer.mod(next, 100)}
  end

  def get_direction(entry) do
    <<dir::binary-size(1), rest::binary>> = entry

    direction =
      case dir do
        "L" -> "L"
        "R" -> "R"
      end

    {direction, Integer.parse(rest)}
  end

  # part1(lines)
  def part1(lines) do
    count = 0
    start = 50
    {_curr, count} = Enum.reduce(lines, {start, count}, fn line, {curr, count} ->
      # Rotate each line that comes in
      # Count each 0,
      {direction, {amount,_}} = get_direction(line)
      {_mod_count, curr} = mod_rotate(curr, amount, direction)
      if curr == 0 do
        {curr, count + 1}
      else
        {curr, count}
      end
    end)
    count
  end

  # part2(lines)
  def part2(lines) do
    count = 0
    start = 50
    {_curr, count} = Enum.reduce(lines, {start, count}, fn line, {curr, count} ->
      # Rotate each line that comes in
      # Count each 0,
      {direction, {amount,_}} = get_direction(line)
      {mod_count, curr} = mod_rotate(curr, amount, direction)

      {curr, count + mod_count}
    end)
    count
  end

  # main entrypoint
  def main do
    filename = get_input_file()

    IO.puts("Part 1:")
    lines = prep(filename)
    IO.puts("\tAnswer: #{part1(lines)}")

    IO.puts("\nPart 2:")
    lines2 = prep(filename)
    IO.puts("\tAnswer: #{part2(lines2)}")
  end
end

# Run main automatically when executed as a script
Day.main()
