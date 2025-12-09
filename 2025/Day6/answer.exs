defmodule Day do
  Code.require_file("utils/util.ex")

  def impl(lines) do
    Enum.reduce(lines, [], fn line, arrays ->
      arrays ++ [String.split(line)]
    end) |> Enum.zip() |> Enum.map(&Tuple.to_list/1)
  end

  def find_dimensions(ops, lines, arr) do
    {_, rest} = String.split_at(ops, 1)
    if String.trim(rest) === "" do
      size = String.length(rest)+1
      Enum.reduce(Enum.with_index(lines), arr, fn {line, index}, acc ->
        str = String.graphemes(String.slice(line, 0, size))
        List.replace_at(acc, index, Enum.at(acc, index) ++ [str])
      end)
    else
      #find the distance from the first opp to the next opp
      [dimension, a, b]= String.split(rest, ~r{\*|\+}, include_captures: true, parts: 2)
      size = String.length(dimension)

      arr = Enum.reduce(Enum.with_index(lines), arr, fn {line, index}, acc ->
        str = String.graphemes(String.slice(line, 0, size))
        List.replace_at(acc, index, Enum.at(acc, index) ++ [str])
      end)
      rest_lines = Enum.map(lines, fn line -> String.slice(line, size+1, String.length(line)-size) end)
      find_dimensions(Enum.join([a,b]), rest_lines, arr)
    end
  end

  def impl3(lines) do
    lines = Enum.reverse(lines)
    [ops | rest] = lines
    { String.split(ops),Enum.reverse(find_dimensions(ops, rest, [[],[],[],[]]))}
  end

   def operators(operator, numbers) do
    case operator do
      "*" -> Enum.reduce(numbers, &*/2)
      "+" -> Enum.reduce(numbers, &+/2)
    end
  end

  def split_line_on_first_space_before_content(line) do
    String.split(line, ~r{' \s'})
  end

  def execute(arrays) do
    Enum.reduce(arrays, 0, fn (array, acc) ->
      [operator | numbers] = Enum.reverse(array)
      val =operators(operator, Enum.map(numbers, &String.to_integer/1))
      acc + val
    end)
  end

  def cephalopods_endian(list) do
   # find the max string length
   # padd all other strings to the max length with 0
   # take each number from index in string and concat together to form a new string
   # convert that to an integer

   Enum.reduce(list, [], fn(row, acc) ->
    # ["123", " 45", "  6"]
    mathed = Enum.map(Enum.zip(row), fn(x) ->
      String.to_integer(String.trim(Enum.join(Tuple.to_list(x))))
    end)
    acc ++ [mathed]
    end)

  end

  def part1(lines) do
    arr = impl(lines)
    execute(arr)
  end

  def part2(lines) do
    {ops, rows} = impl3(lines)
    to_ceph = rows |> Enum.zip() |> Enum.map(&Tuple.to_list/1)
    from_ceph = cephalopods_endian(to_ceph)
    Enum.reduce(Enum.zip(ops, from_ceph), 0, fn ({op, num}, acc) -> acc+operators(op, num) end)
  end

  # main entrypoint
  def main do
    lines = Util.get_input_lines(System.argv(), __ENV__.file() |> Path.dirname(), false)
    IO.puts("Part 1: #{part1(lines)}")
    IO.puts("Part 2: #{part2(lines)}")
  end
end

# Run main automatically when executed as a script
Day.main()
