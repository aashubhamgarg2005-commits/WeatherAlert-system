import HistoryTable from "../../components/tables/HistoryTable";

function History() {
  return (
    <div className="space-y-6">

      <h1 className="text-3xl font-bold">
        Historical Weather Data
      </h1>

      {/* Future upgrade point: filters */}
      {/* <HistoryFilters /> */}

      <HistoryTable />

    </div>
  );
}

export default History;