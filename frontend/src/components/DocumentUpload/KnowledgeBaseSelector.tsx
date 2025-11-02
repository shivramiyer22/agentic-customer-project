/**
 * KnowledgeBaseSelector dropdown populated from /collections endpoint
 * with "Auto-Map" as default option
 */

'use client';

import { useState, useEffect } from 'react';
import { useUploadContext } from '@/context/UploadContext';
import { uploadApi } from '@/services/api-client';
import { cn } from '@/utils/cn';

interface Collection {
  name: string;
  display_name: string;
}

export default function KnowledgeBaseSelector() {
  const { uploadState, setTargetCollection } = useUploadContext();
  const [collections, setCollections] = useState<Collection[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadCollections();
  }, []);

  const loadCollections = async () => {
    setLoading(true);
    try {
      const response = await uploadApi.getCollections() as { collections?: string[] };
      
      // Map collections to display format
      const collectionList: Collection[] = [
        { name: 'auto-map', display_name: 'Auto-Map' },
        ...(response.collections || []).map((name: string) => ({
          name,
          display_name: name
            .split('_')
            .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' '),
        })),
      ];
      
      setCollections(collectionList);
      
      // Set Auto-Map as default
      if (!uploadState.targetCollection) {
        setTargetCollection('auto-map');
      }
    } catch (error) {
      console.error('Failed to load collections:', error);
      // Fallback to default collections
      setCollections([
        { name: 'auto-map', display_name: 'Auto-Map' },
        { name: 'billing_knowledge_base', display_name: 'Billing Knowledge Base' },
        { name: 'technical_knowledge_base', display_name: 'Technical Knowledge Base' },
        { name: 'policy_knowledge_base', display_name: 'Policy Knowledge Base' },
      ]);
      setTargetCollection('auto-map');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-2">
      <label htmlFor="collection-select" className="text-sm font-semibold text-gray-700">
        Target Knowledge Base
      </label>
      <select
        id="collection-select"
        value={uploadState.targetCollection || 'auto-map'}
        onChange={(e) => setTargetCollection(e.target.value || null)}
        disabled={loading}
        className={cn(
          'w-full px-3 py-2 border border-gray-300 rounded-lg',
          'focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
          'disabled:bg-gray-100 disabled:cursor-not-allowed'
        )}
        aria-label="Select knowledge base collection"
      >
        {collections.map((collection) => (
          <option key={collection.name} value={collection.name}>
            {collection.display_name}
          </option>
        ))}
      </select>
      <p className="text-xs text-gray-500">
        {uploadState.targetCollection === 'auto-map'
          ? 'Documents will be automatically categorized based on content'
          : `Documents will be uploaded to ${uploadState.targetCollection}`}
      </p>
    </div>
  );
}

