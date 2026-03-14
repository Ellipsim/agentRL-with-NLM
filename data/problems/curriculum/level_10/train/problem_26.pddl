

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b7)
(on b2 b6)
(on b3 b9)
(on b4 b2)
(on-table b5)
(on-table b6)
(on b7 b8)
(on b8 b11)
(on b9 b10)
(on b10 b12)
(on b11 b4)
(on b12 b5)
(clear b1)
(clear b3)
)
(:goal
(and
(on b1 b5)
(on b2 b6)
(on b3 b10)
(on b5 b7)
(on b7 b11)
(on b10 b2)
(on b11 b12)
(on b12 b4))
)
)


