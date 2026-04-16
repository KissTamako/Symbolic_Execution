(set-logic ALL)
; Constraint ID: 9f18746bd04484da
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60073)) (False)
(assert (not (not (= x 60073))))

(check-sat)
(get-model)
