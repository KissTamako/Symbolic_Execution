(set-logic ALL)
; Constraint ID: f2076be95889aaab
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60547)) (False)
(assert (not (= x 60547)))

; Query: ((== x 60548)) (False)
(assert (not (not (= x 60548))))

(check-sat)
(get-model)
