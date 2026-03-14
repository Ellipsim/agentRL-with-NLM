

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b4)
(on b3 b1)
(on-table b4)
(on b5 b8)
(on-table b6)
(on b7 b11)
(on b8 b10)
(on b9 b7)
(on-table b10)
(on b11 b5)
(clear b3)
(clear b6)
(clear b9)
)
(:goal
(and
(on b1 b11)
(on b2 b4)
(on b4 b9)
(on b5 b6)
(on b8 b2)
(on b9 b5)
(on b11 b10))
)
)


