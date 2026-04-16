(set-logic ALL)
; Constraint ID: ad7fe1555d6456d3
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59392)) (False)
(assert (not (= x 59392)))

; Query: ((== x 59393)) (False)
(assert (not (not (= x 59393))))

(check-sat)
(get-model)
