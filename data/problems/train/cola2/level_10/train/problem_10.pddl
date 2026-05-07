

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b4)
(on b3 b1)
(ontable b4)
(on b5 b8)
(ontable b6)
(on b7 b11)
(on b8 b10)
(on b9 b7)
(ontable b10)
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


