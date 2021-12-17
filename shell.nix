{ pkgs ? import <nixpkgs> {} }:
let
  packages = with pkgs.rPackages; [ ggplot2 ggthemes rmarkdown knitr ];
  r = (pkgs.rWrapper.override {inherit packages;});
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    r
    (pkgs.rstudioWrapper.override {inherit packages;})
    (pkgs.writers.writeDashBin "knitr" ''
      [ $# -eq 2 ] || exit 1

      extension="$1"
      input="$2"
      output="$(basename "$input" .Rmd)"

      [ "$extension" = html -o "$extension" = pdf ] || exit 1

      ${r}/bin/R --no-restore -e "rmarkdown::render('$input',output_file='$output.$extension')" >/dev/null
    '')
    (python3.withPackages (p: [
      p.pandas
      p.jupyter
      p.matplotlib
    ]))
  ];
  shellHook = "export HISTFILE=${toString ./.history}";
}
