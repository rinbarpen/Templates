@echo off

echo reference: https://davyjones2010.github.io/2023-03-05-head-first-revealjs/

#reveal.js
git clone https://github.com/hakimel/reveal.js.git
cd reveal.js
npm install
npm start

cd ..
#pandoc
curl -o ./ https://github.com/jgm/pandoc/releases/tag/3.1.9/pandoc-3.1.9-windows-x86_64.zip
tar -zxvf pandoc-3.1.9-windows-x86_64.zip
cd pandoc-3.1.9-windows-x86_64
npm install

cd ..
#tailwindcss
npm install -D tailwindcss
npx tailwindcss init
