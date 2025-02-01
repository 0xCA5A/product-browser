{ pkgs }:

pkgs.mkShell {

  buildInputs = with pkgs; [
    python313Packages.pip
    pipenv

    nodejs
  ];
}
