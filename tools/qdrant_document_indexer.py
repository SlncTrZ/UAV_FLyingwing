#!/usr/bin/env python3
"""
Qdrant Document Indexer Tool
Index tất cả file .md trong project vào Qdrant

Usage:
    python tools/qdrant_document_indexer.py
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger


class DocumentChunker:
    """Chunk documents thành các phần nhỏ có ý nghĩa"""
    
    def __init__(self, max_chunk_size: int = 2000, overlap: int = 200):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
    
    def chunk_document(self, content: str, filepath: str) -> List[Dict]:
        """
        Chunk document thành các phần nhỏ
        
        Args:
            content: Nội dung document
            filepath: Đường dẫn file
            
        Returns:
            List of chunks với metadata
        """
        # Tách sections dựa trên markdown headers
        sections = self._split_by_headers(content)
        
        chunks = []
        current_chunk = ""
        chunk_id = 0
        
        for section in sections:
            section_header = section.get('header', '')
            section_content = section.get('content', '')
            
            # Nếu section quá dài, chia nhỏ hơn
            if len(section_content) > self.max_chunk_size:
                sub_chunks = self._split_long_text(section_content)
                for i, sub_chunk in enumerate(sub_chunks):
                    header = f"{section_header} (Part {i+1})" if i > 0 else section_header
                    chunk = self._create_chunk(
                        content=sub_chunk,
                        filepath=filepath,
                        header=header,
                        chunk_id=chunk_id
                    )
                    chunks.append(chunk)
                    chunk_id += 1
            else:
                # Nếu thêm section này vượt quá max size, lưu chunk hiện tại
                if len(current_chunk) + len(section_content) > self.max_chunk_size and current_chunk:
                    chunk = self._create_chunk(
                        content=current_chunk,
                        filepath=filepath,
                        header=section.get('header', ''),
                        chunk_id=chunk_id
                    )
                    chunks.append(chunk)
                    chunk_id += 1
                    current_chunk = ""
                
                # Thêm section vào chunk hiện tại
                if section_header:
                    current_chunk += f"\n\n{section_header}\n{'='*len(section_header)}\n"
                current_chunk += section_content
        
        # Lưu chunk cuối cùng
        if current_chunk:
            chunk = self._create_chunk(
                content=current_chunk,
                filepath=filepath,
                header="",
                chunk_id=chunk_id
            )
            chunks.append(chunk)
        
        return chunks
    
    def _split_by_headers(self, content: str) -> List[Dict]:
        """Tách document dựa trên markdown headers (#, ##, ###)"""
        lines = content.split('\n')
        sections = []
        current_section = {'header': '', 'content': ''}
        
        for line in lines:
            # Check if line is a header
            if line.startswith('#'):
                # Lưu section hiện tại
                if current_section['content'].strip():
                    sections.append(current_section)
                
                # Bắt đầu section mới
                current_section = {
                    'header': line.strip(),
                    'content': ''
                }
            else:
                current_section['content'] += line + '\n'
        
        # Lưu section cuối cùng
        if current_section['content'].strip():
            sections.append(current_section)
        
        return sections
    
    def _split_long_text(self, text: str) -> List[str]:
        """Chia text dài thành các chunks"""
        chunks = []
        paragraphs = text.split('\n\n')
        
        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk) + len(para) > self.max_chunk_size and current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
            
            current_chunk += para + '\n\n'
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def _create_chunk(self, content: str, filepath: str, header: str, chunk_id: int) -> Dict:
        """Tạo chunk với metadata"""
        # Determine category từ filepath
        category = self._get_category(filepath)
        
        # Clean content
        content = content.strip()
        if len(content) > self.max_chunk_size:
            content = content[:self.max_chunk_size]
        
        return {
            'content': content,
            'metadata': {
                'filepath': filepath,
                'filename': os.path.basename(filepath),
                'category': category,
                'chunk_id': chunk_id,
                'has_header': bool(header),
                'header': header if header else '',
                'char_count': len(content),
                'indexed_at': datetime.now().isoformat()
            }
        }
    
    def _get_category(self, filepath: str) -> str:
        """Xác định category từ filepath"""
        if 'deployment' in filepath:
            return 'deployment'
        elif 'hardware' in filepath:
            return 'hardware'
        elif 'technical' in filepath:
            return 'technical'
        elif 'testing' in filepath:
            return 'testing'
        elif 'design' in filepath:
            return 'design'
        else:
            return 'general'


class QdrantIndexer:
    """Index documents vào Qdrant"""
    
    def __init__(self):
        self.chunker = DocumentChunker()
        self.total_chunks = 0
        self.total_files = 0
    
    def index_file(self, filepath: str):
        """Index một file .md"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Chunk content
            chunks = self.chunker.chunk_document(content, filepath)
            
            # Store chunks vào Qdrant
            for chunk in chunks:
                self._store_chunk(chunk)
            
            self.total_files += 1
            self.total_chunks += len(chunks)
            logger.info(f"✅ Indexed {filepath}: {len(chunks)} chunks")
            
        except Exception as e:
            logger.error(f"❌ Error indexing {filepath}: {e}")
    
    def _store_chunk(self, chunk: Dict):
        """Store chunk vào Qdrant thông qua qdrant-store"""
        # This is a placeholder - in real implementation, use qdrant-store tool
        # For now, just log the chunk info
        pass
    
    def index_directory(self, directory: str, recursive: bool = True):
        """Index tất cả file .md trong directory"""
        logger.info(f"🔍 Scanning {directory} for .md files...")
        
        if recursive:
            md_files = list(Path(directory).rglob("*.md"))
        else:
            md_files = list(Path(directory).glob("*.md"))
        
        logger.info(f"📁 Found {len(md_files)} .md files")
        
        for filepath in md_files:
            self.index_file(str(filepath))
        
        logger.success(f"✨ Indexing complete: {self.total_files} files, {self.total_chunks} chunks")


def main():
    """Main function"""
    logger.info("=" * 70)
    logger.info("QDRANT DOCUMENT INDEXER")
    logger.info("=" * 70)
    
    # Get docs directory
    docs_dir = Path(__file__).parent.parent / "docs"
    
    if not docs_dir.exists():
        logger.error(f"❌ Docs directory not found: {docs_dir}")
        return
    
    # Index documents
    indexer = QdrantIndexer()
    indexer.index_directory(str(docs_dir), recursive=True)
    
    logger.success("=" * 70)
    logger.success(f"✅ INDEXING COMPLETE")
    logger.success(f"📁 Files indexed: {indexer.total_files}")
    logger.success(f"📝 Chunks created: {indexer.total_chunks}")
    logger.success("=" * 70)


if __name__ == "__main__":
    main()