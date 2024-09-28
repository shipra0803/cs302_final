#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <cstdlib>  // For srand() and rand()
#include <ctime>    // For time()

using namespace std;

vector<vector<int> > grid = {
    {7, 8, 0, 4, 0, 0, 1, 2, 0},
    {6, 0, 0, 0, 7, 5, 0, 0, 9},
    {0, 0, 0, 6, 0, 1, 0, 7, 8},
    {0, 0, 7, 0, 4, 0, 2, 6, 0},
    {0, 0, 1, 0, 5, 0, 9, 3, 0},
    {9, 0, 4, 0, 6, 0, 0, 0, 5},
    {0, 7, 0, 3, 0, 0, 0, 1, 2},
    {1, 2, 0, 0, 0, 7, 4, 0, 0},
    {0, 4, 9, 2, 0, 6, 0, 0, 7}
};

void drawGrid(sf::RenderWindow &window) {
    float width = 500.0f;
    float height = 500.0f;
    float cellSize = width / 9;

    // Draw the cells
    for (int i = 0; i < 9; ++i) {
        for (int j = 0; j < 9; ++j) {
            // Draw cell background
            sf::RectangleShape cell(sf::Vector2f(cellSize, cellSize));
            cell.setPosition(i * cellSize, j * cellSize);
            cell.setFillColor(sf::Color::White);

            // Draw grid lines
            if (grid[i][j] != 0) {
                cell.setFillColor(sf::Color(200, 200, 200));  // Light gray for filled cells
            }
            window.draw(cell);
        }
    }

    // Draw vertical and horizontal grid lines
    for (int i = 0; i <= 9; ++i) {
        // Vertical lines
        sf::Vertex verticalLine[] =
        {
            sf::Vertex(sf::Vector2f(i * cellSize, 0), sf::Color::Black),
            sf::Vertex(sf::Vector2f(i * cellSize, height), sf::Color::Black)
        };
        window.draw(verticalLine, 2, sf::Lines);

        // Horizontal lines
        sf::Vertex horizontalLine[] =
        {
            sf::Vertex(sf::Vector2f(0, i * cellSize), sf::Color::Black),
            sf::Vertex(sf::Vector2f(width, i * cellSize), sf::Color::Black)
        };
        window.draw(horizontalLine, 2, sf::Lines);
    }

    // Draw numbers
    sf::Font font;
    if (!font.loadFromFile("/Users/juanitahernandez/Downloads/BigCaslon.ttf")) { // Load a font, make sure the font file is available
        std::cerr << "Could not load font!" << std::endl;
        return;
    }
    
    sf::Text text;
    text.setFont(font);
    text.setCharacterSize(40); // Set the font size
    text.setFillColor(sf::Color::Black); // Set text color

    for (int i = 0; i < 9; ++i) {
        for (int j = 0; j < 9; ++j) {
            if (grid[i][j] != 0) {
                text.setString(std::to_string(grid[i][j]));
                text.setPosition(i * cellSize + cellSize / 4, j * cellSize + cellSize / 8); // Adjust text position
                window.draw(text);
            }
        }
    }
}

int main() {
    sf::RenderWindow window(sf::VideoMode(500, 500), "Sudoku Grid");

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear(sf::Color::White);
        drawGrid(window);
        window.display();
    }

    return 0;
}