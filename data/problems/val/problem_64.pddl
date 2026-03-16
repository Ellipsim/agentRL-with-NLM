

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b4)
(on b3 b2)
(on b4 b1)
(ontable b5)
(on b6 b8)
(on b7 b11)
(on b8 b10)
(on b9 b7)
(ontable b10)
(ontable b11)
(clear b3)
(clear b6)
(clear b9)
)
(:goal
(and
(on b1 b5)
(on b2 b10)
(on b4 b2)
(on b5 b3)
(on b7 b6)
(on b8 b9)
(on b9 b7)
(on b10 b11)
(on b11 b1))
)
)


