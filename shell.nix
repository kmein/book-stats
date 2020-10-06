{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = with pkgs; [
    (python3.withPackages (p: [
      p.pandas
      p.jupyter
      p.matplotlib
    ]))
  ];
  shellHook = "export HISTFILE=${toString ./.history}";
}
