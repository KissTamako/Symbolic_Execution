(set-logic ALL)
; Constraint ID: d3f67662e4f20e11
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60445)) (False)
(assert (not (= x 60445)))

; Query: ((== x 60446)) (False)
(assert (not (not (= x 60446))))

(check-sat)
(get-model)
