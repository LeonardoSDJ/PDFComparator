# PDFComparator

[Português](#português) | [English](#english)

## Português

### Visão Geral

PDFComparator é uma ferramenta desenvolvida em Python para comparar arquivos PDF, identificando diferenças tanto no conteúdo visual quanto textual. Esta aplicação pode ser útil para profissionais que necessitam realizar revisões detalhadas em documentos PDF, como editores, revisores legais ou qualquer pessoa que precise comparar versões de documentos PDF.

### Funcionalidades

- **Comparação de Imagens**  
  Gera imagens comparativas destacando as diferenças de pixels entre dois arquivos PDF. Utiliza sobreposições coloridas para indicar áreas com diferenças.

- **Comparação de Texto**  
  Marca o texto reconhecível nos PDFs com máscaras coloridas:  
  - Verde: Texto inalterado  
  - Laranja: Alterações na fonte ou cor  
  - Vermelho: Texto adicionado ou modificado  

- **Interface Gráfica Intuitiva**  
  Facilita a seleção de arquivos e visualização das diferenças. Controles para ajuste de contraste, brilho e intensidade das diferenças.

- **Geração de Relatórios**  
  Cria relatórios detalhados das diferenças encontradas.

### Requisitos

- Python 3.8 ou superior
- Bibliotecas: numpy, opencv-python, PyMuPDF, Pillow

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/LeonardoSDJ/PDFComparator.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd PDFComparator
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Uso

#### Via Interface Gráfica

Execute o arquivo `main.py`:
```bash
python main.py
```

#### Via Linha de Comando

```bash
python -m pdfcomparator "/caminho/para/arquivo1.pdf" "/caminho/para/arquivo2.pdf" "/pasta/de/saida/"
```

**Opções:**
- `--cache` ou `-c`: Especifica um caminho para cache, acelerando comparações futuras.

### Construindo um Executável

Para criar um executável standalone:

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Execute o PyInstaller:
   ```bash
   pyinstaller main.py --name PDFComparator --windowed --icon=path_to_your_icon.ico
   ```

O executável será gerado na pasta `dist`.

### Contribuindo

Contribuições são bem-vindas! Por favor, leia as diretrizes de contribuição antes de submeter pull requests.

### Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

### Agradecimentos

Este projeto foi inspirado e baseado no trabalho original de VintLin [aqui](https://github.com/VintLin/pdf-comparator).

---

## English

### Overview

PDFComparator is a tool developed in Python for comparing PDF files, identifying differences in both visual and textual content. This application is particularly useful for professionals who need to perform detailed reviews of PDF documents, such as editors, legal reviewers, or anyone who needs to compare versions of PDF documents.

### Features

- **Image Comparison**  
  Generates comparative images highlighting pixel differences between two PDF files. Uses colored overlays to indicate areas with differences.

- **Text Comparison**  
  Marks recognizable text in the PDFs with colored masks:  
  - Green: Unchanged text  
  - Orange: Changes in font or color  
  - Red: Added or modified text  

- **Intuitive Graphical Interface**  
  Facilitates file selection and visualization of differences. Controls for adjusting contrast, brightness, and intensity of differences.

- **Report Generation**  
  Creates detailed reports of the differences found.

### Requirements

- Python 3.8 or higher
- Libraries: numpy, opencv-python, PyMuPDF, Pillow

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LeonardoSDJ/PDFComparator.git
   ```

2. Navigate to the project directory:
   ```bash
   cd PDFComparator
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Via Graphical Interface

Run the `main.py` file:
```bash
python main.py
```

#### Via Command Line

```bash
python -m pdfcomparator "/path/to/file1.pdf" "/path/to/file2.pdf" "/output/folder/"
```

**Options:**
- `--cache` or `-c`: Specifies a cache path, speeding up future comparisons.

### Building a Standalone Executable

To create a standalone executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run PyInstaller:
   ```bash
   pyinstaller main.py --name PDFComparator --windowed --icon=path_to_your_icon.ico
   ```

The executable will be generated in the `dist` folder.

### Contributing

Contributions are welcome! Please read the contribution guidelines before submitting pull requests.

### License

This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgments

This project was inspired and based on the original work by VintLin [here](https://github.com/VintLin/pdf-comparator).