{ pkgs }:

let

  java = pkgs.jdk17_headless;

in

pkgs.mkShell {

  buildInputs = with pkgs; [
    python310Packages.pip
    pipenv

    nodejs
  ];
}
