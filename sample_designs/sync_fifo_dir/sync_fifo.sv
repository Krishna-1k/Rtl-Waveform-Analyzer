module sync_fifo #(
    parameter DATA_WIDTH = 8,
    parameter DEPTH = 4
) (
    input  logic                  clk,
    input  logic                  rst_n,
    input  logic                  wr_en,
    input  logic                  rd_en,
    input  logic [DATA_WIDTH-1:0] din,
    output logic [DATA_WIDTH-1:0] dout,
    output logic                  full,
    output logic                  empty
);

    localparam ADDR_WIDTH = $clog2(DEPTH);

    logic [DATA_WIDTH-1:0] fifo [0:DEPTH-1];
    logic [ADDR_WIDTH:0]   wr_ptr, rd_ptr;
    logic                  fifo_full, fifo_empty;

    // Write logic
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wr_ptr <= '0;
        end else if (wr_en && !fifo_full) begin
            fifo[wr_ptr[ADDR_WIDTH-1:0]] <= din;
            wr_ptr <= wr_ptr + 2; //Purposely faulty
        end
    end

    // Read logic
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rd_ptr <= '0;
            dout   <= '0;
        end else if (rd_en && !fifo_empty) begin
            dout   <= fifo[rd_ptr[ADDR_WIDTH-1:0]];
            rd_ptr <= rd_ptr + 1;
        end
    end

    // Status flags
    assign fifo_full  = (wr_ptr - rd_ptr) == DEPTH;
    assign fifo_empty = (wr_ptr == rd_ptr);
    assign full       = fifo_full;
    assign empty      = fifo_empty;
    

endmodule