const express = require('express');
const pug = require('pug');
const fs = require('fs');
const documents = require('./documents')
const documentTemplate = pug.compileFile('document.pug', {filename: __filename})
const app = express();
app.use(express.static('public'));

app.get('/library/', (req, res) => {
    fs.readFile(__dirname + '/index.pug', 'utf8', (err, template) => {
        if (err) throw err
        let response
        const filter = req.query.filter
        if (filter) {
            const sanitized = filter.substring(0, 200).replaceAll('<', '&lt;').replaceAll('>', '&gt;')
            response = template.replace(/filter-value/g, `Searching by ${sanitized}`)
        } else {
            response = template.replace(/filter-value/g, '')
        }
        const docs = documents.getDocuments(filter)
        let html;
        try {
            html = pug.render(response, {documents: docs, filename: __filename});
        } catch (e) {
            html = pug.render(template, {documents: [], error: e.message, filename: __filename})
        }
        res.set('Content-Type', 'text/html')
        res.send(html)
    });
});

app.get('/library/document/:documentId', (req, res) => {
    const documentId = req.params.documentId
    res.set('Content-Type', 'text/html')
    const document = documents.getDocumentById(documentId)
    res.send(documentTemplate({document}))
});

app.get('/library/info/:documentId', (req, res) => {
    const documentId = req.params.documentId
    res.set('Content-Type', 'text/plain')
    const document = documents.getDocumentById(documentId)
    if (document?.moreInfoAvailable) {
        res.send(`More info available at ${document.moreInfoAvailable}. Ask the library administrator to send you the file.`)
    } else {
        res.send('No info available.')
    }
});

app.listen(3000, () => console.log('app listening on 3000'))