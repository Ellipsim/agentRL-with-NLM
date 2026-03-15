

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b3)
(on b2 b6)
(on-table b3)
(on b4 b5)
(on-table b5)
(on b6 b9)
(on b7 b4)
(on-table b8)
(on b9 b11)
(on-table b10)
(on b11 b8)
(clear b1)
(clear b2)
(clear b7)
(clear b10)
)
(:goal
(and
(on b1 b8)
(on b2 b7)
(on b3 b4)
(on b5 b6)
(on b6 b1)
(on b7 b11)
(on b8 b2)
(on b10 b3)
(on b11 b10))
)
)


