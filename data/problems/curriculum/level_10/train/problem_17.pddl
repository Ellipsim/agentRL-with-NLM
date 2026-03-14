

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b10)
(on b2 b11)
(on-table b3)
(on b4 b6)
(on b5 b1)
(on b6 b9)
(on b7 b4)
(on b8 b5)
(on b9 b3)
(on-table b10)
(on-table b11)
(on b12 b7)
(clear b2)
(clear b8)
(clear b12)
)
(:goal
(and
(on b1 b3)
(on b2 b9)
(on b3 b12)
(on b4 b8)
(on b5 b6)
(on b8 b11)
(on b9 b7)
(on b10 b2)
(on b11 b1)
(on b12 b10))
)
)


