defmodule Navigation do
  @moduledoc false

  def north({x, y}, distance \\ 1), do: {x, y - distance}
  def east({x, y}, distance \\ 1),  do: {x + distance, y}
  def south({x, y}, distance \\ 1), do: {x, y + distance}
  def west({x, y}, distance \\ 1),  do: {x - distance, y}

  def in_bounds({x, y}, {max_x, max_y}) do
    x >= 0 and x < max_x and y >= 0 and y < max_y
  end
end