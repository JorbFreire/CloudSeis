import { useEffect, useState } from 'react';
import { TreeItem } from '@mui/x-tree-view/TreeItem';

import api from 'services/api';

interface IDatasetWorkflows {
  workflowId: number
}

export default function DatasetWorkflows({ workflowId }: IDatasetWorkflows) {
  const [datasets, setDatasets] = useState<Array<IWorkflow>>([])

  useEffect(() => {
    const token = localStorage.getItem("jwt")
    if (!token) return

    api.get<Array<IWorkflow>>(`/dataset/list/${workflowId}`, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    }).then((response) => {
      setDatasets(response.data)
    })
  }, [])

  return (
    <>
      {datasets.map((dataset) => (
        <TreeItem
          nodeId={`workflow-${dataset.id}-from-dataset-from-${workflowId}`}
          label={dataset.output_name ? dataset.output_name : `dataset-${dataset.id}`}
          key={dataset.id}
        />
      ))}
    </>
  )
}