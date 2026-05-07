

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b7)
(on b2 b10)
(on b3 b5)
(ontable b4)
(on b5 b8)
(on b6 b9)
(ontable b7)
(ontable b8)
(on b9 b2)
(on b10 b3)
(ontable b11)
(clear b1)
(clear b4)
(clear b6)
(clear b11)
)
(:goal
(and
(on b1 b9)
(on b2 b7)
(on b4 b6)
(on b5 b8)
(on b8 b4)
(on b11 b10))
)
)


