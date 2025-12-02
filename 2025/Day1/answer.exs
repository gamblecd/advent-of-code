defmodule Day do
  Code.require_file("utils/util.ex")
  @moduledoc false

  def mod_rotate(current, amount, "L") do
    next = current - amount
    wrap_and_mod(next, current)
  end

  def mod_rotate(current, amount, "R") do
    next = current + amount
    wrap_and_mod(next, current)
  end

  def wrap_and_mod(next, current) do
    counter =
      cond do
        current == 0 -> 0
        next <= 0    -> 1
        true         -> 0
      end

    {div(abs(next), 100) + counter, Integer.mod(next, 100)}
  end

  def get_direction(entry) do
    <<dir::binary-size(1), rest::binary>> = entry
    {amount, _} = Integer.parse(rest)
    {dir, amount}
  end

  def combined(lines) do
    {_curr, part2, part1} =
      Enum.reduce(lines, {50, 0, 0}, fn line, {curr, part2, part1} ->
        # Rotate each line that comes in
        # Count each 0,
        {direction, amount} = get_direction(line)
        {mod_count, curr} = mod_rotate(curr, amount, direction)

        {curr, part2 + mod_count, if curr == 0 do part1 + 1 else part1 end}
      end)

    IO.puts("Part 1: #{part1}")
    IO.puts("Part 2: #{part2}")
  end

  # main entrypoint
  def main do
    combined(Util.get_input_lines(System.argv(), __ENV__.file() |> Path.dirname()))
  end
end

# Run main automatically when executed as a script
Day.main()
