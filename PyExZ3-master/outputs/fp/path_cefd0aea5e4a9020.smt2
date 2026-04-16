(set-logic ALL)
; Executed Path ID: cefd0aea5e4a9020
; Generated at: 2026-04-16 16:02:54
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const a Int)

; ((== (% a 2) 0)) (True)
(assert (= (mod a 2) 0))
; ((== a (floor se))) (False)
(assert (not (= a (floor se))))

(check-sat)
(get-model)
