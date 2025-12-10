defmodule Day do
  Code.require_file("utils/util.ex")

  def build(lines) do
    Enum.map(lines, fn line ->
      line |> String.split(",") |> Enum.map(fn x -> String.to_integer(x) end) |> List.to_tuple()
    end)
  end

  def x_distance({x1, y1}, {x2, y2}) do
    abs(x2 - x1)+1
  end

  def y_distance({x1, y1}, {x2, y2}) do
    abs(y2 - y1)+1
  end

  def area({x1, y1}, {x2, y2}) do
    x_distance({x1, y1}, {x2, y2}) * y_distance({x1, y1}, {x2, y2})
  end

  def find_opposite_corners(dot,dot2) do
    {{elem(dot, 0), elem(dot2, 1)}, {elem(dot2,0),elem(dot,1)}}
  end

  def impl(dots) do
    # each dot is a point, we need to find the largest size rectange, so find the x distance and y distance and multiply them to get the area, then sort by the size
    sizes = Enum.reduce(dots, %{}, fn dot, acc ->
      Enum.reduce(dots, acc, fn dot2, acc2 ->
        # check to make sure the combination is not ordered
        acc2 = unless Map.has_key?(acc2, {dot, dot2}) or Map.has_key?(acc2, {dot2, dot}) do
            Map.put(acc2, {dot, dot2}, area(dot, dot2))
          else
          acc2
        end
      end)
    end) |>Enum.map(fn {k,v} -> {k,v} end) |> Enum.sort(fn {k1,v1}, {k2,v2} -> v1 > v2 end)
  end

  def create_horizontal_dots_between_points(y, pt1, pt2) do
    # for each integer between the x values, create a dot
    dots = Enum.map(pt1..pt2, fn x -> {x, y} end)
    dots
  end

    def create_vertical_dots_between_points(x, pt1, pt2) do
    # for each integer between the x values, create a dot
    dots = Enum.map(pt1..pt2, fn y -> {x, y} end)
    dots
  end

  def green_dots(dots) do
    Enum.reduce(dots, [], fn dot, acc ->
      Enum.reduce(dots, acc, fn dot2, acc2 ->
        cond do
          x_distance(dot, dot2) == 1 -> acc2 ++ create_vertical_dots_between_points(elem(dot, 0), elem(dot, 1), elem(dot2, 1))
          y_distance(dot, dot2) == 1 -> acc2 ++ create_horizontal_dots_between_points(elem(dot, 1), elem(dot, 0), elem(dot2, 0))
          true ->
            acc2
        end
      end)
    end)
  end

  def part1(lines) do
    sizes = impl(lines)
    [{pt, area}| rest] = sizes
    area
  end

  def find_largest_squares_in_boundary(dots, boundary_points, min_x, min_y) do
    sizes = Enum.reduce(dots, %{}, fn dot, acc ->
      Enum.reduce(dots, acc, fn dot2, acc2 ->
        # check to make sure the combination is not ordered
        acc2 = unless Map.has_key?(acc2, {dot, dot2}) or Map.has_key?(acc2, {dot2, dot}) do
            # check to make sure dot, dot2, and opposite_corners all are in boundary_points
            {dot3, dot4} = find_opposite_corners(dot, dot2)
            acc2 = if dot in boundary_points and dot2 in boundary_points and dot3 in boundary_points and dot4 in boundary_points do
              Map.put(acc2, {dot, dot2}, area(dot, dot2))
            else
              acc2
            end
          else
          acc2
        end
      end)
    end) |>Enum.map(fn {k,v} -> {k,v} end) |> Enum.sort(fn {k1,v1}, {k2,v2} -> v1 > v2 end)
  end

  def is_boundary_dot(dot, boundary_points) do
    dot in boundary_points
  end

  # def is_point_inside(dot, boundary_points, min_x, min_y) do
  #   # figure out from the minimum location a ray that goes through to the point, if the number of points in the way is odd, it is inside
  #   x = elem(dot, 0)
  #   y = elem(dot, 1)
  #   # which is closer to the min_x or min_y
  #   if x - min_x < y - min_y do
  #     # use a horizontal ray



  #   end


  # end

  def grid_boundaries(dots) do
    [dots1|rest] = dots
    [dots2|_] = rest
    Enum.reduce(dots, {elem(dots1, 0), elem(dots1, 1), elem(dots2, 0), elem(dots2, 1)}, fn dot, acc ->
      {min_x, min_y, max_x, max_y} = acc
      {x, y} = dot
      {min(min_x, x), min(min_y, y), max(max_x, x), max(max_y, y)}
    end)
  end

  def part2(lines) do
    red_dots = lines
    green_dots = green_dots(red_dots)
    squares = find_largest_squares_in_boundary(red_dots, green_dots++red_dots, min_x, min_y)
    {min_x, min_y, max_x, max_y} = grid_boundaries(red_dots)
    [{pt, area}| rest] = squares
    IO.puts("#{min_x}, #{min_y}, #{max_x}, #{max_y}")
    Util.print_grid({min_x, min_y}, {max_x, max_y}, ".", [{"X", green_dots}, {"#", red_dots}, {"O", Tuple.to_list(pt)}])
    area
  end

  # main entrypoint
  def main do
    lines = Util.get_input_lines(System.argv(), __ENV__.file() |> Path.dirname())
    data = build(lines)
    IO.puts("Part 1: #{part1(data)}")
    IO.puts("Part 2: #{part2(data)}")
  end
end

# Run main automatically when executed as a script
Day.main()
