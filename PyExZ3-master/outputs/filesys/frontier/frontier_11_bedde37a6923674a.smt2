(set-logic ALL)
; Constraint ID: bedde37a6923674a
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60676)) (False)
(assert (not (= x 60676)))

; Query: ((== x 60677)) (False)
(assert (not (not (= x 60677))))

(check-sat)
(get-model)
