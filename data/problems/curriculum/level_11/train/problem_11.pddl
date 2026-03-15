

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on-table b1)
(on b2 b10)
(on b3 b9)
(on b4 b8)
(on b5 b1)
(on b6 b11)
(on-table b7)
(on b8 b2)
(on b9 b5)
(on b10 b7)
(on b11 b4)
(on b12 b6)
(on b13 b3)
(clear b12)
(clear b13)
)
(:goal
(and
(on b1 b11)
(on b2 b5)
(on b3 b9)
(on b4 b7)
(on b7 b2)
(on b8 b12)
(on b9 b10)
(on b10 b6)
(on b11 b8)
(on b12 b3))
)
)


