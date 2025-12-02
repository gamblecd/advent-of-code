defmodule Util do
  @moduledoc false

  # Elixir version of get_input_file(args, script_dir, filename=None)
  #
  # Usage patterns:
  #   Util.get_input_file(System.argv(), script_dir)
  #   Util.get_input_file(System.argv(), script_dir, some_filename)
  #
  # If filename is non-nil -> always returns "inputs/actual.txt"
  # Else if first arg is "PROD" -> "inputs/actual.txt"
  # Else -> "inputs/ex.txt"
  def get_input_file(args, script_dir) do
    # first arg is filename
    filename =
      if length(args) == 0 do
        "ex.txt"
      else
        case String.upcase(hd(args)) do
          "PROD" -> "actual.txt"
          "TEST" -> "ex.txt"
          _ -> hd(args)
        end
      end
    Path.join([script_dir, "inputs", filename])
  end

  def get_input_lines(args, script_dir) do
    prep(get_input_file(args, script_dir))
  end

  def prep(filename) do
    filename
    |> File.stream!()
    |> Stream.map(&String.trim/1)
    |> Enum.to_list()
  end

  # Simple timing helper similar in spirit to timer_func decorator.
  #
  # Usage:
  #   Util.time_fun(fn -> your_work_here() end, :my_func)
  #
  # Prints: "Function 'my_func' executed in 0.0123s"
  def time_fun(fun, label \\ :anonymous, print_args \\ false, args \\ []) when is_function(fun, 0) do
    t1 = System.monotonic_time(:microsecond)
    result = fun.()
    t2 = System.monotonic_time(:microsecond)
    secs = (t2 - t1) / 1_000_000

    if print_args do
      IO.puts(
        "Function #{inspect(label)}, (#{Enum.map_join(args, ", ", &to_string/1)}) executed in #{Float.round(secs, 4)}s"
      )
    else
      IO.puts("Function #{inspect(label)} executed in #{Float.round(secs, 4)}s")
    end

    result
  end

  # print_grid_basic(grid, sep=" ")
  # grid is list of lists, e.g. [[".", "#"], [".", "."]]
  def print_grid_basic(grid, sep \\ " ") do
    Enum.each(grid, fn row ->
      row
      |> Enum.map(&to_string/1)
      |> Enum.join(sep)
      |> IO.puts()
    end)
  end

  # print_grid(min, max, basic_char, overlays)
  # min = {xmin, ymin}, max = {xmax, ymax}
  # basic_char is the default char for all cells
  # overlays = [{char_or_fun, points_list}, ...]
  def print_grid({xmin, ymin} = min, {xmax, ymax}, basic_char, overlays) do
    offset = min

    grid =
      for _y <- ymin..ymax do
        for _x <- xmin..xmax do
          basic_char
        end
      end

    grid_with_overlays =
      Enum.reduce(overlays, grid, fn {char, lst}, acc ->
        Enum.reduce(lst, acc, fn {px, py} = point, acc2 ->
          x = px - elem(offset, 0)
          y = py - elem(offset, 1)

          value =
            if is_function(char, 1) do
              char.(point)
            else
              char
            end

          List.update_at(acc2, y, fn row ->
            List.replace_at(row, x, value)
          end)
        end)
      end)

    # Build index rows (max 99) similar to Python version
    x_range = xmin..xmax
    grid_with_indexes = build_x_index_rows(x_range, grid_with_overlays)

    Enum.each(Enum.with_index(grid_with_indexes, ymin), fn
      {row, y_index} when is_list(row) ->
        # normal grid row: add y index
        IO.puts("#{to_string(y_index) |> String.pad_leading(3)} " <> Enum.join(Enum.map(row, &to_string/1)))

      {row, _} when is_binary(row) ->
        # index rows are already strings
        IO.puts(row)
    end)
  end

  defp build_x_index_rows(x_range, grid) do
    xmax = Enum.max(x_range)
    _xmin = Enum.min(x_range)

    if div(xmax + 1, 10) >= 2 do
      x_lines = List.duplicate(["    "], div(xmax + 1, 10))

      x_lines =
        Enum.reduce(x_range, x_lines, fn i, acc ->
          if rem(i, 5) == 0 do
            ones = List.last(acc)

            ones =
              List.update_at(ones, -1, fn
                _ when i < 0 -> "-"
                v -> v
              end)

            ones = ones ++ [Integer.to_string(rem(i, 10))]

            acc =
              List.update_at(acc, -1, fn _ -> ones end)

            if i >= 10 do
              tens = Enum.at(acc, -2) ++ [Integer.to_string(div(i, 10))]
              List.update_at(acc, -2, fn _ -> tens end)
            else
              tens = Enum.at(acc, -2) ++ [" "]
              List.update_at(acc, -2, fn _ -> tens end)
            end
          else
            Enum.map(acc, fn line -> line ++ [" "] end)
          end
        end)

      Enum.map(x_lines, &Enum.join/1) ++ grid
    else
      grid
    end
  end

  # BFS_search equivalent.
  #
  # Options:
  #  :get_heap_item  (fn x -> x end)
  #  :end_condition  (fn x -> length(x.children) == 0 end)
  #  :returner       (fn item, weight, visited -> item end)
  #  :get_children   (fn x -> x.children end)
  #  :get_visitor    (fn x -> x end)
  #  :get_weight     (fn x -> x.weight end)
  def bfs_search(initial, opts \\ []) do
    get_heap_item = Keyword.get(opts, :get_heap_item, & &1)
    end_condition = Keyword.get(opts, :end_condition, fn x -> Map.get(x, :children, []) == [] end)
    returner = Keyword.get(opts, :returner, fn x, _w, _v -> x end)
    get_children = Keyword.get(opts, :get_children, &Map.get(&1, :children, []))
    get_visitor = Keyword.get(opts, :get_visitor, & &1)
    get_weight = Keyword.get(opts, :get_weight, &Map.get(&1, :weight, 0))

    start = {0, get_heap_item.(initial), []}
    queue = [start]
    do_bfs(queue, [], [], end_condition, returner, get_children, get_visitor, get_weight, get_heap_item)
  end

  defp do_bfs([], _visited_overall, paths, _end_cond, _ret, _get_children, _get_visitor, _get_weight, _ghi),
    do: Enum.reverse(paths)

  defp do_bfs([{weight, item, visited} | rest], visited_overall, paths,
              end_cond, ret, get_children, get_visitor, get_weight, get_heap_item) do
    paths =
      if end_cond.(item) do
        [ret.(item, weight, visited) | paths]
      else
        paths
      end

    {new_queue, new_visited_overall} =
      Enum.reduce(get_children.(item), {rest, visited_overall}, fn child, {q, vo} ->
        visitor = get_visitor.(child)

        if visitor in visited or visitor in vo do
          {q, vo}
        else
          new_item = get_heap_item.(child)
          new_weight = weight + get_weight.(child)
          # simple priority queue: keep list sorted by weight
          new_q = insert_by_weight({new_weight, new_item, visited ++ [visitor]}, q)
          {new_q, [visitor | vo]}
        end
      end)

    do_bfs(new_queue, new_visited_overall, paths, end_cond, ret, get_children, get_visitor, get_weight, get_heap_item)
  end

  defp insert_by_weight(elem, queue) do
    {w, _i, _v} = elem

    {before, next} =
      Enum.split_while(queue, fn {w2, _i2, _v2} -> w2 <= w end)

    before ++ [elem] ++ next
  end
end
