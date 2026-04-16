(set-logic ALL)
; Constraint ID: 55a32d93f5bc1f49
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59917)) (False)
(assert (not (not (= x 59917))))

(check-sat)
(get-model)
