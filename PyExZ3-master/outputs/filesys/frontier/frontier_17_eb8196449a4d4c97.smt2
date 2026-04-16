(set-logic ALL)
; Constraint ID: eb8196449a4d4c97
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60685)) (False)
(assert (not (= x 60685)))

; Query: ((== x 60686)) (False)
(assert (not (not (= x 60686))))

(check-sat)
(get-model)
