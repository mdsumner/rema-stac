library(remav2)
x <- remav2_index()
make_p <- function(x) {
  if (is.recursive(x)) x <- unlist(x)
  y <- x[3:4]
  x <- x[1:2]
  #cbind(x[c(1, 2, 2, 1, 1)], y[c(1, 1, 2, 2, 1)])
  cbind(x[c(1, 2, 2, 1, 1)], y[c(2, 2, 1, 1, 2)])
}
library(dplyr)
p <- make_p(x |> slice(1) |> select(xmin, xmax, ymin, ymax))
read_json <- function(x) {
  yyjsonr::from_json_conn(url(x))
}

## s3url is no good we need the bit after /#/
#s3url <- x$s3url[1]
#https://pgc-opendata-dems.s3.us-west-2.amazonaws.com/rema/mosaics/v2.0/2m/06_37.json
json <- x |> slice(1) |> transmute(jsonurl = sprintf("https:/%s", substr(s3url, gregexpr("/#/external", s3url)[[1]] + 11, nchar(s3url)))
) |> pull(jsonurl) |> read_json()
reproj::reproj_xy(p, "OGC:CRS84", source = "EPSG:3031")
json$geometry$coordinates

