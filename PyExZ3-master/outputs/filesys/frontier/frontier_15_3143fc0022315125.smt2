(set-logic ALL)
; Constraint ID: 3143fc0022315125
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60457)) (False)
(assert (not (= x 60457)))

; Query: ((== x 60458)) (False)
(assert (not (not (= x 60458))))

(check-sat)
(get-model)
