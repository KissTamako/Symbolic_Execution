(set-logic ALL)
; Constraint ID: dc336e7968caa45f
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59236)) (False)
(assert (not (= x 59236)))

; Query: ((== x 59237)) (False)
(assert (not (not (= x 59237))))

(check-sat)
(get-model)
