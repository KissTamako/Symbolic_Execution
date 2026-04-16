(set-logic ALL)
; Constraint ID: d18941fbb2ed73f9
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59338)) (False)
(assert (not (= x 59338)))

; Query: ((== x 59339)) (False)
(assert (not (not (= x 59339))))

(check-sat)
(get-model)
