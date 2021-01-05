let
  pkgs = import <nixpkgs> { overlays = [ ]; };
in
  with pkgs;
  mkShell {
    buildInputs = with python38Packages; [
      pandas
      xlrd
      requests
    ];
}
