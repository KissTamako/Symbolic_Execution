(set-logic ALL)
; Constraint ID: 553b69e0d2e54d48
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59335)) (False)
(assert (not (not (= x 59335))))

(check-sat)
(get-model)
