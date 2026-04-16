(set-logic ALL)
; Constraint ID: c189a3334a18ff5f
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59482)) (False)
(assert (not (= x 59482)))

; Query: ((== x 59483)) (False)
(assert (not (not (= x 59483))))

(check-sat)
(get-model)
