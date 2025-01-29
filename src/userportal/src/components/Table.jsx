import React, { useEffect } from 'react';
import { useTable, useSortBy } from 'react-table';

const Table = ({ columns, data, loading, onSortChange, enableSorting = false }) => {
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    state: { sortBy }
  } = useTable({ columns, data }, enableSorting ? useSortBy : undefined);

  useEffect(() => {
    if (enableSorting) {
      onSortChange(sortBy);
    }
  }, [sortBy, enableSorting]);

  return (
    <div>
      <table {...getTableProps()} className="table">
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()} key={headerGroup.id}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps(enableSorting ? column.getSortByToggleProps() : undefined)} key={column.id}>
                  {column.render('Header')}
                  {enableSorting && (
                  <span>
                    {column.isSorted
                      ? column.isSortedDesc
                        ? <i className="ms-2 fas fa-sort-down text-muted"></i>
                        : <i className="ms-2 fas fa-sort-up text-muted"></i>
                      : <i className="ms-2 fas fa-sort text-muted"></i>}
                  </span>
                  )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="text-center">No records to display</td>
            </tr>
          ) : (
          rows.map(row => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()} key={row.index}>
                {row.cells.map(cell => (
                  <td {...cell.getCellProps()} key={cell.column.id}>
                    {cell.render('Cell')}
                  </td>
                ))}
              </tr>
            );
          })
        )}
        </tbody>
      </table>
      {loading && <div>Loading...</div>}
    </div>
  );
};

export default Table;