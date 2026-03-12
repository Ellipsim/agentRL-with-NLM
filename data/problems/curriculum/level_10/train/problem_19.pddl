

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on-table b1)
(on b2 b7)
(on b3 b2)
(on b4 b9)
(on-table b5)
(on b6 b1)
(on b7 b6)
(on b8 b11)
(on b9 b8)
(on b10 b3)
(on-table b11)
(clear b4)
(clear b5)
(clear b10)
)
(:goal
(and
(on b1 b9)
(on b2 b4)
(on b3 b6)
(on b4 b8)
(on b6 b7)
(on b7 b11)
(on b8 b1)
(on b10 b2)
(on b11 b10))
)
)


