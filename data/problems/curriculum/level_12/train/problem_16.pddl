

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b13)
(on b2 b12)
(on b3 b1)
(on b4 b10)
(on b5 b2)
(on b6 b4)
(on-table b7)
(on b8 b9)
(on b9 b3)
(on-table b10)
(on-table b11)
(on b12 b8)
(on b13 b6)
(clear b5)
(clear b7)
(clear b11)
)
(:goal
(and
(on b3 b9)
(on b4 b11)
(on b5 b13)
(on b8 b7)
(on b9 b12)
(on b11 b10)
(on b12 b5)
(on b13 b6))
)
)


