defmodule Day1 do
  @moduledoc false

  # Determine input file:
  # - if an argument is given: use that as the filename
  # - otherwise default to "actual.txt" in the same directory as the script
  def get_input_file do
    case System.argv() do
      [filename | _] ->
        filename

      [] ->
        script_dir =
          __ENV__.file()
          |> Path.dirname()

        Path.join(Path.join(script_dir, "inputs"), "actual.txt")
    end
  end

  # prep() -> lines
  def prep(filename) do
    filename
    |> File.stream!()
    |> Stream.map(&String.trim/1)
    |> Enum.to_list()
  end

  def counter(value) do
    count = 0
    curry = fn amount -> if amount == value do ^count = (count + 1) end end

    {curry, fn -> count end}
  end

  def mod_rotate(current, amount, direction) do
    IO.puts("#{current} #{amount} #{direction}")
    next =
      if direction == "L" do
        current - amount
      else
        current + amount
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
    direction =
      if String.slice(entry, 0, 1) == "L" do
        "L"
      else
        "R"
      end

    {direction, Integer.parse(String.slice(entry, 1, String.length(entry)))}
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
      IO.puts("#{_mod_count}, #{curr}")
      if curr == 0 do
        {curr, count + 1}
      else
        {curr, count}
      end
    end)

    IO.write("Part 1: ")
    IO.puts("Answer: #{count}")
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
      IO.puts("#{mod_count}, #{curr}")

      {curr, count + mod_count}
    end)

    IO.write("Part 2: ")
    IO.puts("Answer: #{count}")
  end

  # main entrypoint
  def main do
    filename = get_input_file()

    lines = prep(filename)
    part1(lines)

    IO.puts("")

    lines2 = prep(filename)
    part2(lines2)
  end
end

# Run main automatically when executed as a script
Day1.main()
