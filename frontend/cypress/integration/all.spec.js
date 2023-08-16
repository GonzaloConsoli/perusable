
describe('Perusable', function () {
    it('Displays the home page.', function () {
        cy.visit('/');
        cy.get('h1').should('contain', 'Perusable');
    });

    it('Displays a list of results.', function () {
        cy.intercept('GET', '**/api/v1/catalog/wines/**', { fixture: 'wines.json' }).as('getWines');

        cy.visit('/');
        cy.get('input#country').type('US');
        cy.get('input#points').type('92');
        cy.get('input#query').type('staglin');
        cy.get('button').contains('Search').click();
        cy.wait('@getWines');
        cy.get('div.card-title').should('contain', 'Cabernet Sauvignon');
    });
});