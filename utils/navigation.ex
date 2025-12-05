defmodule Navigation do
  @moduledoc false

  def north({x,y}) do north({x,y}, 1) end
  def north({x, y}, distance \\ 1), do: {x, y - distance}
  def east({x,y}) do east({x,y}, 1) end
  def east({x, y}, distance \\ 1),  do: {x + distance, y}
  def south({x,y}) do south({x,y}, 1) end
  def south({x, y}, distance \\ 1), do: {x, y + distance}
  def west({x,y}) do west({x,y}, 1) end
  def west({x, y}, distance \\ 1),  do: {x - distance, y}
  def northwest({x,y}) do northwest({x,y}, 1) end
  def northwest({x, y}, distance \\ 1), do: {x - distance, y - distance}
  def northeast({x,y}) do northeast({x,y}, 1) end
  def northeast({x, y}, distance \\ 1), do: {x + distance, y - distance}
  def southwest({x,y}) do southwest({x,y}, 1) end
  def southwest({x, y}, distance \\ 1), do: {x - distance, y + distance}
  def southeast({x,y}) do southeast({x,y}, 1) end
  def southeast({x, y}, distance \\ 1), do: {x + distance, y + distance}

  def cardinal_dirs, do: [&Navigation.north/1, &Navigation.east/1, &Navigation.south/1, &Navigation.west/1]
  def diagonal_dirs, do: [&Navigation.northeast/1, &Navigation.southeast/1, &Navigation.southwest/1, &Navigation.northwest/1]
  def dirs, do: cardinal_dirs() ++ diagonal_dirs()
  def in_bounds({x, y}, {max_x, max_y}) do
    x >= 0 and x < max_x and y >= 0 and y < max_y
  end
end
