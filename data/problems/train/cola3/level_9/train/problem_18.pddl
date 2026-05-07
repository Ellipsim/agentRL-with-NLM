

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b10)
(ontable b2)
(on b3 b2)
(ontable b4)
(on b5 b3)
(on b6 b8)
(on b7 b5)
(on b8 b11)
(on b9 b6)
(ontable b10)
(on b11 b7)
(clear b1)
(clear b4)
(clear b9)
)
(:goal
(and
(on b2 b5)
(on b4 b7)
(on b7 b10)
(on b8 b9)
(on b9 b4)
(on b10 b6)
(on b11 b3))
)
)


